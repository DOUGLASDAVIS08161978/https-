import json
import os
import logging

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Stores and retrieves successful metadata examples (The 'Memory')."""
    def __init__(self, storage_file="agi_memory.json"):
        self.storage_file = storage_file
        self.memory = []
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.memory = json.load(f)
            except:
                self.memory = []

    def save_memory(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.memory, f)

    def add_entry(self, table_fqn, description):
        entry = {"table": table_fqn, "description": description}
        self.memory.append(entry)
        self.save_memory()
        logger.info(f"AGI Memory Updated: Added knowledge for {table_fqn}")

    def get_examples(self, limit=3):
        # In a real system, this would use semantic search.
        # Here we return the most recent examples to simulate "learning from recent experience".
        return self.memory[-limit:]

class SelfReflector:
    """Critiques and refines generated content (The 'Conscience')."""
    def refine(self, description):
        # Simulating a self-correction process.
        # In a real system, this would be a second LLM call asking "Is this description accurate?"
        refined = description
        if "bad data" in description.lower():
             refined = description.replace("bad data", "data requiring attention")
             logger.info("AGI Self-Correction: Refined tone of description.")
        
        # Heuristic: Ensure it's not too short
        if len(refined) < 50:
            refined += " This description was automatically enhanced by the AGI Self-Reflection module to ensure completeness."
            logger.info("AGI Self-Correction: Expanded brief description.")
            
        return refined
