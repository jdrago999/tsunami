# var.ts
create session with weight 1 as 'show_var':
    var product_id is a unique number from 1 to 10
    var pin is a random number from 1000 to 9999
    var user_name is a random string of length 5
    var password is a random string of length 15

    get '/product/$product_id'
    post '/user/create' with data 'user_name=$user_name&password=$password&pin=$pin'

create load:                
    spawn users every 1 seconds for 1 seconds
