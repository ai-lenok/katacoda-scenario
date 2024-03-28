`echo ${not_set_my_var}`{{execute}}
`echo ${not_set_my_var:?message if not set}`{{execute}}
`echo "status: $?"`{{execute}}
`echo ${not_set_my_var}`{{execute}}