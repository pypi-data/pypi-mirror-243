from datetime import timedelta

from odoo import api, fields, models, _


class HrAttendanceValidationSheet(models.Model):
    _inherit = "hr.attendance.validation.sheet"

    def name_get(self):
        results = []
        for rec in self:
            results.append(
                (
                    rec.id,
                    _("[%s] %s - %s")
                    % (
                        rec.date_from.strftime("%Y"),
                        rec.date_from.strftime("%B"),
                        rec.employee_id.name,
                    ),
                )
            )
        return results

    def _default_from_date(self):
        """returns the fist day of the past month"""
        today = fields.Date.today()
        month = today.month - 1 if today.month > 1 else 12
        return today.replace(day=1, month=month)

    def _default_to_date(self):
        """returns last day of previous month"""
        today = fields.Date.today()
        return today.replace(day=1) - timedelta(days=1)

    date_from = fields.Date(
        string="Date from",
        required=True,
        default=_default_from_date,
    )

    date_to = fields.Date(
        string="Date to",
        required=True,
        default=_default_to_date,
    )

    diff_hours = fields.Float(
        string="Difference (hours)",
    )

    @api.onchange("employee_id", "date_from", "date_to")
    def _default_calendar_id(self):
        """returns the calendar of the employee for the month of the validation sheet"""
        if not self.employee_id:
            return
        month = self.date_from.month
        year = self.date_from.year
        cal = self.employee_id.resource_calendar_id.hours_per_day
        external_id = f"hr_attendance_mitxelena.calendar_{year}_{month}_{cal}h"
        cal_id = self.env["ir.model.data"].xmlid_to_res_id(external_id)
        calendar_external_id = self.env["resource.calendar"].search(
            [("id", "=", cal_id)]
        )
        return {"value": {"calendar_id": calendar_external_id.id}}

    calendar_id = fields.Many2one(
        "resource.calendar",
        string="Calendar",
        required=True,
        related="",
        default=_default_calendar_id,
    )

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
        ondelete="cascade",
        index=True,
    )

    mother_calendar_id = fields.Many2one(
        "resource.calendar",
        string="Resource Calendar",
        related="employee_id.mother_calendar_id",
        readonly=True,
        store=False,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    theoretical_hours = fields.Float(
        string="Theoretical (hours)",
        related="calendar_id.total_hours",
        help="Theoretical calendar hours to spend by week.",
    )

    attendance_hours = fields.Float(
        "Attendance (hours)",
        compute="_compute_attendances_hours",
        help="Compute number of attendance lines not marked as overtime",
    )
    attendance_total_hours = fields.Float(
        "Total Attendance (hours)",
        compute="_compute_attendances_hours",
        help="Validated attendances. Sum attendance and due overtime lines.",
    )
    overtime_due_hours = fields.Float(
        "Overtime due (hours)",
        compute="_compute_attendances_hours",
        help="Compute number of attendance lines marked as overtime which are marked as due",
    )
    overtime_not_due_hours = fields.Float(
        "Overtime not due (hours)",
        compute="_compute_attendances_hours",
        help="Compute number of attendance lines marked as overtime which are not due",
    )

    relevo_days = fields.Integer(
        string="Relevo days",
        help="Number of days the employee has work in a relevo entry type",
        compute="_compute_relevo_days",
    )
    nights_worked = fields.Float(
        string="Nights worked",
        help="Number of nights the employee has worked",
        compute="_compute_nights_worked",
    )

    def _compute_nights_worked(self):
        for record in self:
            entire_nights_worked = len(
                record.attendance_ids.filtered(
                    lambda att: att.shift_type == "night" and not att.is_overtime
                )
            )
            overtime_nights_worked = (
                sum(
                    record.attendance_ids.filtered(
                        lambda att: att.shift_type == "night" and att.is_overtime
                    ).mapped("worked_hours")
                )
                / record.calendar_id.hours_per_day
            )

            record.nights_worked = entire_nights_worked + overtime_nights_worked

    @api.depends("attendance_ids.is_relevo")
    def _compute_relevo_days(self):
        for record in self:
            # Here we need to extract the number of unique days the employee has
            # worked in a relevo entry type.

            # First we get the attendance lines that are relevo
            relevo_attendances = record.attendance_ids.filtered(
                lambda att: att.is_relevo
            )

            # Then we get the unique days of the attendance entries
            unique_days = set(att.check_in.date().day for att in relevo_attendances)

            # Finally we get the number of unique days
            record.relevo_days = len(unique_days)

    @api.model
    def generate_reviews(self):
        reviews = self.env["hr.attendance.validation.sheet"]
        month = self._default_from_date().month
        year = self._default_from_date().year
        for employee in self.env["hr.employee"].search([("active", "=", True)]):
            cal = employee.resource_calendar_id.hours_per_day
            external_id = f"hr_attendance_mitxelena.calendar_{year}_{month}_{cal}h"
            calendar_id = self.env["ir.model.data"].xmlid_to_res_id(external_id)

            reviews += self.create(
                {
                    "employee_id": employee.id,
                    "calendar_id": calendar_id,
                }
            )
        reviews.action_retrieve_attendance_and_leaves()
        return reviews

    # This function will need to be overriden in order to compute the leave hours
    # in case the leave is not recorded by hours or half days, as it recomputes
    # the hours based on the calendar attendances and week days.
    @api.depends("leave_ids")
    def _compute_leaves(self):
        for record in self:
            leave_hours = 0
            for leave in record.leave_ids:
                if leave.request_unit_half or leave.request_unit_hours:
                    # we assume time off is recorded by hours
                    leave_hours += leave.number_of_hours_display
                else:
                    current_date = max(leave.request_date_from, record.date_from)
                    date_to = min(
                        leave.request_date_to or leave.request_date_from, record.date_to
                    )
                    while current_date <= date_to:
                        # we sum the hours per day from calendar if it is a working day
                        # TODO: check how to handle when it is a time off day
                        # (holiday or global time off)
                        if current_date.weekday() < 5:
                            leave_hours += record.calendar_id.hours_per_day
                        current_date += timedelta(days=1)

            record.leave_hours = leave_hours

    # This function will need to be overriden in order to compute the
    # attendance hours using the extra_time_with_factor.
    @api.depends("attendance_ids", "attendance_ids.is_overtime")
    def _compute_attendances_hours(self):
        for record in self:
            record.attendance_hours = sum(
                record.attendance_ids.filtered(lambda att: not att.is_overtime).mapped(
                    "worked_hours"
                )
            )
            record.overtime_due_hours = sum(
                record.attendance_ids.filtered(
                    lambda att: att.is_overtime and att.is_overtime_due
                ).mapped("extra_time_with_factor")
            )
            record.overtime_not_due_hours = sum(
                record.attendance_ids.filtered(
                    lambda att: att.is_overtime and not att.is_overtime_due
                ).mapped("extra_time_with_factor")
            )
            record.attendance_total_hours = sum(
                record.attendance_due_ids.filtered(lambda att: att.is_overtime).mapped(
                    "extra_time_with_factor"
                )
                + record.attendance_ids.filtered(
                    lambda att: not att.is_overtime
                ).mapped("worked_hours")
            )

    def _round_hours(self, hours):
        entire_hours = int(hours)
        minutes = hours - entire_hours
        if minutes < 0.33:
            minutes = 0
        elif minutes < 0.66:
            minutes = 0.5
        else:
            minutes = 1
        return entire_hours + minutes

    def _compute_default_compensatory_hour(self):
        super()._compute_default_compensatory_hour()
        for record in self:
            record.diff_hours = record.compensatory_hour - record.regularization_compensatory_hour_taken
            record.compensatory_hour = record._round_hours(record.compensatory_hour)
            record.regularization_compensatory_hour_taken = record._round_hours(
                record.regularization_compensatory_hour_taken
            )
