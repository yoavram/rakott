from rakott.scripts import todaystr

def test_todaystr():
	today = todaystr()
	assert isinstance(today, str)
	assert todaystr
