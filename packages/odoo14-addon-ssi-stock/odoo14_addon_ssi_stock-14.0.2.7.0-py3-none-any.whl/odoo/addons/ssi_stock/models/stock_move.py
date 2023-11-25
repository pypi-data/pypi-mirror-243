# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = ["stock.move"]

    forced_lot_id = fields.Many2one("stock.production.lot")

    def _get_available_quantity(
        self,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
        allow_negative=False,
    ):
        if not lot_id and self.forced_lot_id and self.location_id.usage == "internal":
            lot_id = self.forced_lot_id
        return super()._get_available_quantity(
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
            allow_negative=allow_negative,
        )

    def _update_reserved_quantity(
        self,
        need,
        available_quantity,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=True,
    ):
        if not lot_id and self.forced_lot_id and self.location_id.usage == "internal":
            lot_id = self.forced_lot_id
        return super()._update_reserved_quantity(
            need,
            available_quantity,
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
        )

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        res = super()._prepare_merge_moves_distinct_fields()
        return res + ["forced_lot_id"]

    @api.onchange(
        "picking_type_id",
    )
    def onchange_procure_method(self):
        if self.picking_type_id:
            self.procure_method = self.picking_type_id.procure_method
