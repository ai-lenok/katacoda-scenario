`echo ${check_if_set}`{{execute}}
`echo ${check_if_set:+variable set}`{{execute}}
`echo ${check_if_set}`{{execute}}
`check_if_set="10"`{{execute}}
`echo ${check_if_set:+variable set}`{{execute}}