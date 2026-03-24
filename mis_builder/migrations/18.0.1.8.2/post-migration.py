# Copyright 2026 Ledo Enterprises
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Recompute source_aml_model_id on mis.report.instance.period.

    This stored computed field was introduced in 18.0 but existing periods
    from earlier versions have NULL values, causing drilldown to fail with
    'No view found for act_window action undefined'.
    """
    cr.execute(
        """
        UPDATE mis_report_instance_period p
        SET source_aml_model_id = r.move_lines_source
        FROM mis_report_instance i
        JOIN mis_report r ON r.id = i.report_id
        WHERE p.report_instance_id = i.id
          AND p.source_aml_model_id IS NULL
          AND r.move_lines_source IS NOT NULL
        """
    )
    _logger.info(
        "Recomputed source_aml_model_id on %d mis.report.instance.period records",
        cr.rowcount,
    )
