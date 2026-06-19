from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SITE_URL = "https://homezh-aiyouxi.com.cn"
CORE_TAG = "爱游戏"


@dataclass
class KeywordNote:
    """单个关键词笔记的数据结构"""
    keyword: str
    note: str
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat(timespec='seconds')

    def short_display(self) -> str:
        """简短的单行显示"""
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] {self.note[:30]}... | 标签: {tag_str}"

    def full_report(self) -> str:
        """完整的多行格式化输出"""
        lines = [
            f"关键词: {self.keyword}",
            f"笔记内容: {self.note}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"记录时间: {self.created_at}",
            f"来源站点: {SITE_URL}",
            "-" * 40
        ]
        return "\n".join(lines)


@dataclass
class KeywordNotesCollection:
    """管理一组关键词笔记"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, keyword: str, note: str, tags: Optional[List[str]] = None):
        new_note = KeywordNote(keyword=keyword, note=note, tags=tags or [])
        self.notes.append(new_note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def list_all_short(self) -> List[str]:
        return [note.short_display() for note in self.notes]

    def export_full_text(self) -> str:
        blocks = [note.full_report() for note in self.notes]
        header = f"关键词笔记集合 (来源: {SITE_URL}, 核心标签: {CORE_TAG})\n"
        header += "=" * 50 + "\n"
        return header + "\n".join(blocks)


def format_notes_for_markdown(collection: KeywordNotesCollection) -> str:
    """将笔记集合输出为友好的 Markdown 格式"""
    lines = [f"# 关键词笔记 - {CORE_TAG}", f"站点: {SITE_URL}", ""]
    if not collection.notes:
        lines.append("_暂无笔记_")
        return "\n".join(lines)

    for idx, note in enumerate(collection.notes, 1):
        lines.append(f"## {idx}. {note.keyword}")
        lines.append(f"**笔记**: {note.note}")
        if note.tags:
            tags_str = ", ".join(f"`{t}`" for t in note.tags)
            lines.append(f"**标签**: {tags_str}")
        lines.append(f"**创建时间**: {note.created_at}")
        lines.append("")

    lines.append(f"---\n*生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    return "\n".join(lines)


def demo_usage():
    """创建一个示例笔记集合并展示各种输出方式"""
    collection = KeywordNotesCollection()

    collection.add_note(
        "爱游戏",
        "这是一个专注于游戏资讯和评测的站点，内容涵盖手游、端游和主机游戏。",
        tags=["游戏门户", "评测"]
    )
    collection.add_note(
        "最新手游推荐",
        "每周更新热门手游榜单，帮助玩家发现好玩的手机游戏。",
        tags=["手游", "推荐"]
    )
    collection.add_note(
        "PC游戏配置",
        "提供主流PC游戏的硬件配置要求，方便玩家升级电脑。",
        tags=["PC", "硬件", "指南"]
    )

    print("=== 简短列表 ===")
    for line in collection.list_all_short():
        print(line)

    print("\n=== 完整报告 ===")
    print(collection.export_full_text())

    print("\n=== Markdown 格式 ===")
    print(format_notes_for_markdown(collection))


if __name__ == "__main__":
    demo_usage()