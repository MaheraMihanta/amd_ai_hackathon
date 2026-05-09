import unittest

from app import find_article, load_inventory, prepare_selection
from llm_assistant import build_pharmacist_context
from vision import process_image


class StockSimulationTest(unittest.TestCase):
    def setUp(self):
        self.inventory = load_inventory()

    def test_find_article_by_id(self):
        article = find_article(self.inventory, "MED-001")

        self.assertIsNotNone(article)
        self.assertEqual(article.nom, "Paracetamol 500mg")

    def test_find_article_by_unique_partial_name(self):
        article = find_article(self.inventory, "amoxicilline")

        self.assertIsNotNone(article)
        self.assertEqual(article.id_unique, "MED-003")

    def test_prepare_selection_success(self):
        result = prepare_selection(self.inventory, "MED-002", 2)

        self.assertTrue(result.ok)
        self.assertEqual(result.code, "SELECTION_OK")
        self.assertIn("Robot allant au compartiment: Rayon A2", result.messages)

    def test_prepare_selection_rejects_unknown_article(self):
        result = prepare_selection(self.inventory, "Produit inexistant", 1)

        self.assertFalse(result.ok)
        self.assertEqual(result.code, "ARTICLE_INTROUVABLE")

    def test_prepare_selection_rejects_insufficient_stock(self):
        result = prepare_selection(self.inventory, "MED-003", 999)

        self.assertFalse(result.ok)
        self.assertEqual(result.code, "STOCK_INSUFFISANT")

    def test_prepare_selection_rejects_invalid_quantity(self):
        result = prepare_selection(self.inventory, "MED-003", 0)

        self.assertFalse(result.ok)
        self.assertEqual(result.code, "QUANTITE_INVALIDE")

    def test_vision_integration_point_is_explicitly_disabled(self):
        result = process_image("images/paracetamol_500mg.svg")

        self.assertFalse(result.enabled)
        self.assertIn("Module vision non configure", result.message)

    def test_llm_context_keeps_pharmacist_validation(self):
        context = build_pharmacist_context("fievre et douleur", self.inventory)
        text = context.as_text()

        self.assertIn("assistant pour pharmacien", text)
        self.assertIn("fievre et douleur", text)
        self.assertIn("Ne pas delivrer automatiquement", text)


if __name__ == "__main__":
    unittest.main()
