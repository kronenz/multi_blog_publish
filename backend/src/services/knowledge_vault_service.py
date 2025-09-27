from typing import Dict, List
from uuid import UUID
from backend.src.models.knowledge_vault import KnowledgeVault

class KnowledgeVaultService:
    def __init__(self):
        self.knowledge_vaults: Dict[UUID, KnowledgeVault] = {}

    def create_knowledge_vault(self, knowledge_vault: KnowledgeVault) -> KnowledgeVault:
        self.knowledge_vaults[knowledge_vault.id] = knowledge_vault
        return knowledge_vault

    def get_knowledge_vault_by_id(self, knowledge_vault_id: UUID) -> KnowledgeVault | None:
        return self.knowledge_vaults.get(knowledge_vault_id)
