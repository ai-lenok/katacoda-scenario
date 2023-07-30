package sbercode

allow[msg] {
	res := input[key]
	res == "OK"
	msg := sprintf("%s: %s", [key, res])
}

deny[msg] {
	res := input[key]
	startswith(res, "FAIL")
	msg := sprintf("%s", substring(res,5))
}


error[msg] {
	res := input[key]
    res != "OK"
    not startswith(res, "FAIL")
    msg := sprintf("%s: %s", [key, res])
}