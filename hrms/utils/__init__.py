from collections.abc import Generator
import requests, calendar
from datetime import date

import frappe
from frappe.utils import add_days, date_diff

country_info = {}


@frappe.whitelist(allow_guest=True)
def get_country(fields=None):
	global country_info
	ip = frappe.local.request_ip

	if ip not in country_info:
		fields = ["countryCode", "country", "regionName", "city"]
		res = requests.get(
			"https://pro.ip-api.com/json/{ip}?key={key}&fields={fields}".format(
				ip=ip, key=frappe.conf.get("ip-api-key"), fields=",".join(fields)
			)
		)

		try:
			country_info[ip] = res.json()

		except Exception:
			country_info[ip] = {}

	return country_info[ip]


def get_date_range(start_date: str, end_date: str) -> list[str]:
	"""returns list of dates between start and end dates"""
	no_of_days = date_diff(end_date, start_date) + 1
	return [add_days(start_date, i) for i in range(no_of_days)]


def generate_date_range(
	start_date: str, end_date: str, reverse: bool = False
) -> Generator[str, None, None]:
	no_of_days = date_diff(end_date, start_date) + 1

	date_field = end_date if reverse else start_date
	direction = -1 if reverse else 1

	for n in range(no_of_days):
		yield add_days(date_field, direction * n)


def get_employee_email(employee_id: str) -> str | None:
	employee_emails = frappe.db.get_value(
		"Employee",
		employee_id,
		["prefered_email", "user_id", "company_email", "personal_email"],
		as_dict=True,
	)

	return (
		employee_emails.prefered_email
		or employee_emails.user_id
		or employee_emails.company_email
		or employee_emails.personal_email
	)


def get_all_date_in_month(month, year):
	num_date = calendar.monthrange(year, month)[1]
	results = [date(year, month, day) for day in range(1, num_date + 1)]
	return results


def config_env_service():
  isProduction = False # Change False if run on env development
  services = {
		"msteam_bot": "https://acerp-bot-team-dev.pandion.vn/api/notification",
		"server_ip": "192.168.11.22"
	}

  if isProduction:
    services = {
		"msteam_bot": "https://acerp-bot-team.pandion.vn/api/notification",
		"server_ip": "192.168.11.23"
	}
  
  return services
