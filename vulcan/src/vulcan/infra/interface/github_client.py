import base64
from http.client import responses

import requests
from typing import Dict, Any
import logging

from litellm.llms.custom_httpx.http_handler import headers
from nltk.chunk.named_entity import shape
from requests import Response
from typer.cli import state

from aireview.domain.entities.pull_request import PullRequest
from aireview.domain.entities.pull_request_file import PullRequestFile
from aireview.domain.entities.review import Review
import logging

logger = logging.getLogger(__name__)

class GitHubClient:

    def __init__(self, pat: str, owner: str, repo: str, base_url: str = "https://api.github.com"):
        self._pat = pat
        self.owner = owner
        self.repo = repo
        self._base_url = base_url.rstrip('/')
        self._session = requests.Session()
        self._headers = {
            "Authorization": f"Bearer {pat}",
            "Accept": "application/vnd.github.v3+json",
            'X-GitHub-Api-Version': '2022-11-28'
        }

    async def get_pull_request(self, pr_number: int) -> PullRequest:
        pr_data = self._session.get(f"{self._base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}")
        pr_data.raise_for_status()

        files_data = self._session.get(f"{self._base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/files")
        files_data.raise_for_status()
        json_pr_data = pr_data.json()

        return PullRequest(
            id=json_pr_data["id"],
            number=json_pr_data["number"],
            title=json_pr_data["title"],
            description=json_pr_data["body"] or "",
            files=[PullRequestFile.from_json(f) for f in files_data.json()],
            base_branch=json_pr_data["base"]["ref"],
            head_branch=json_pr_data["head"]["ref"],
            state= json_pr_data["state"],
            draft= json_pr_data["draft"]
        )

    async def submit_review(
            self,
            pr_number: int,
            review: Review
    ) -> None:
        response: Response
        try:
            logger.info(f"Submit review to pull request #{pr_number}")
            for comment in review.comments:
                logger.info(f"comment: {comment}")
                content = self.get_file_content(comment.file_path, str(pr_number))
                if content is not None:
                    if self.len_content_lines(content) <= int(comment.line):
                        comment.line = self.len_content_lines(content) - 1
                    review_data = {
                        "body": f"**{comment.type}**: {comment.content}",
                        "commit_id": f"5eef9663ece9ea8db44396099bedf1dbbe33d75f",
                        "path": comment.file_path,
                        "start_line": comment.line,
                        "start_side": 'RIGHT',
                        "line": int(comment.line) + 1,
                        "side": 'RIGHT'
                    }

                    response = self._session.post(f"{self._base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/comments",headers=self._headers, json=review_data)

            logger.info(f"Successfully submitted review for PR #{pr_number}")
            logger.info(f"Successfully submitted review for PR #{pr_number} :: response {response.json()}")
        except Exception as e:
            logger.error(f"Failed to submit review for PR #{pr_number}: {str(e)}")
            raise

    def get_file_content(
            self,
            path: str,
            ref: str
    ) -> str:
        try:
            response = self._session.get(f"{self._base_url}/repos/{self.owner}/{self.repo}/contents/{path}",
                                         headers=self._headers,
                                         data={"ref": ref}
                                         )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch file content for {path}: {str(e)}")

    def get_diff_stats(
            self,
            pr_number: int
    ) -> Dict[str, Any]:
        files_data = self._session.get(f"{self._base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/files", headers=self._headers,)
        files_data.raise_for_status()
        return {
            "total_changes": sum(f["changes"] for f in files_data),
            "additions": sum(f["additions"] for f in files_data),
            "deletions": sum(f["deletions"] for f in files_data),
            "changed_files": len(files_data.json())
        }

    def len_content_lines(self, file_content):
        content = file_content.get("content", "")
        if not content:
            return 0

        decoded_content = base64.b64decode(content).decode('utf-8')
        return len(decoded_content.splitlines())