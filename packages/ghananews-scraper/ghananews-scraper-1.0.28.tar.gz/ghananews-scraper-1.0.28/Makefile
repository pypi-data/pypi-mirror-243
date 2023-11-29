release:
	rm -rf build dist
	python setup.py sdist bdist_wheel
	twine upload dist/* --verbose --username __token__ --password pypi-AgEIcHlwaS5vcmcCJDAzMDQxODNmLTkzNzYtNDhlNS05NmFhLTQzYjY0Mzg1MWJhYQACGVsxLFsiZ2hhbmFuZXdzLXNjcmFwZXIiXV0AAixbMixbIjY2NzEwNzNhLTJhYTctNDFlYS05NjVjLWMxNmQ0MTk5NjJkOSJdXQAABiDprAdAQH8Tyr5sAo-dKbvVe9DNkM4pcDnsaiA-pu9MCw

lint:
	pylint --recursive=y ghanaweb myjoyonline yen graphiconline citionline threenews

install:
	pip install -e .

format:
	black *.py

sort:
	isort *.py