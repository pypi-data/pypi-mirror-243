# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class StockMoveLine(models.Model):
    _name = "stock.move.line"
    _inherit = ["stock.move.line"]

    def _assign_auto_lot_number(self):
        self.ensure_one()

        if self.product_id.tracking == "none":
            return True

        if self.lot_name or self.lot_id:
            return True

        if not self.product_id.categ_id.sequence_id:
            return True

        sequence = self.product_id.categ_id.sequence_id
        if self.move_id.date_backdating:
            ctx = {"ir_sequence_date": self.move_id.date_backdating}
            number = sequence.with_context(ctx).next_by_id()
        else:
            number = sequence.next_by_id()
        self.write(
            {
                "lot_name": number,
            }
        )
