# requests.ts
create session with weight 4 as 'request_example':
    get all "/"
    delete '/bookmarks/1234'
    post '/view/create/' with data 'name=view2&value=foo'
        ensure match /^{"success": "View 'view2' created"}$/

create load:
    spawn users every 1 seconds for 1 minutes


