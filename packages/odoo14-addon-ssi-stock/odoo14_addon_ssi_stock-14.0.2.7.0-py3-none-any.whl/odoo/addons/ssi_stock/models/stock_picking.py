# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking"]

    picking_type_category_id = fields.Many2one(
        string="Picking Type Category",
        related="picking_type_id.category_id",
        store=True,
    )
    show_price_unit = fields.Boolean(
        string="Show Price Unit",
        related="picking_type_id.show_price_unit",
        store=False,
    )
    show_procure_method = fields.Boolean(
        string="Show Procure Method",
        related="picking_type_id.show_procure_method",
        store=False,
    )
    allowed_source_location_ids = fields.Many2many(
        string="Allowed Source Locations",
        comodel_name="stock.location",
        related="picking_type_id.allowed_source_location_ids",
        store=False,
    )
    allowed_destination_location_ids = fields.Many2many(
        string="Allowed Destination Locations",
        comodel_name="stock.location",
        related="picking_type_id.allowed_destination_location_ids",
        store=False,
    )
    allowed_product_category_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        related="picking_type_id.allowed_product_category_ids",
        store=False,
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        related="picking_type_id.allowed_product_ids",
        store=False,
    )

    def _assign_auto_lot_number(self):
        for record in self:
            if record.picking_type_id.use_create_lots:
                for line in record.mapped("move_line_ids").filtered(
                    lambda x: (
                        not x.lot_id
                        and not x.lot_name
                        and x.product_id.tracking != "none"
                        and x.product_id.categ_id.sequence_id
                        and x.qty_done != 0.0
                    )
                ):
                    line._assign_auto_lot_number()

    def _action_done(self):
        self._assign_auto_lot_number()
        return super()._action_done()

    def button_validate(self):
        self._assign_auto_lot_number()
        return super().button_validate()
