from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Metadata:
    """
    Metadata 分为：
    - common：通用技术元数据
    - domain：业务领域元数据
    """

    common: Dict[str, Any] = field(default_factory=dict)
    domain: Dict[str, Any] = field(default_factory=dict)

    def get_common(self, key: str, default=None):
        return self.common.get(key, default)

    def get_domain(self, key: str, default=None):
        return self.domain.get(key, default)