# using.ts
create session with weight 1 as 'test_file':
    using view_name, view_value from 'views.csv' randomly
    post '/view/create?name=$view_name&value=$view_value'
create load:                
    spawn users every 1 seconds for 1 seconds
