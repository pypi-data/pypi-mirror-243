
from odoo import models, fields, api

class HrAttendanceValidationSheet(models.AbstractModel):
    _name = 'report.hr_attendance_mitxelena.hr_attendance_validation_sheet'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Retrieve the data from the model HrAttendanceValidationSheet
        records = self.env['hr.attendance.validation.sheet'].browse(docids)

        # Prepare the data to be passed to the report template
        report_data = {
            'records': records,
        }

        return report_data
