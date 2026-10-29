"""论文来源的统一接口，方便以后接入 OpenReview、ACL Anthology 等。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from gleaner.models import Paper


class SourceError(Exception):
    """从论文来源获取数据失败。"""


@dataclass
class Announcement:
    """最近一个公告周期的公告。"""

    papers: list[Paper]  # 符合配置的论文（按需去掉交叉投递、旧论文的新版本）
    entries: int  # 过滤前的公告条数；0 表示这个周期没有公告

    @property
    def empty(self) -> bool:
        return self.entries == 0


class Source(Protocol):
    name: str

    def fetch_latest(self) -> list[Paper]:
        """返回最近一个公告周期的新论文。没有新公告时返回空列表。"""
        ...

    def fetch_announcement(self) -> Announcement:
        """和 fetch_latest 相同，另外给出过滤前的公告条数，用来区分没有公告和都被过滤掉。"""
        ...

    def fetch_recent(self, limit: int) -> list[Paper]:
        """返回最近提交的 limit 篇论文，不区分公告日（没有新公告时补抓或试运行）。"""
        ...
