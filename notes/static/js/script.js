$(document).ready(function(){
    
        $(".vote").click(function(){
            let id,btn,classes,disable,state;
             id = $(this).val()
             btn = $(this)
             classes = ".count"+id
             let val = parseInt($(classes).text())
           if($(this).hasClass('upvote')){
                state = "upvote"
                val = val+1
                disable = $(this).next()  
           }
           else{
                state = "downvote"
                val = val-1
                disable = $(this).prev()  
    
           }
           
           $(classes).text(val)
    
           
           
            $.ajax(
                {
                    type:"POST",
                    enctype: 'multipart/form-data',
                    url: `/details/${id}`,
                    data:{
                        csrfmiddlewaretoken: window.CSRF_TOKEN,
                         'notesid' : id, 
                         'val' : val,
                         'state' : state
                         
                    },
                    datatype:'json',
                    success: function( data ) 
                    {
                        console.log('succass',id)
                        $(btn).prop('disabled', true);
                        $(disable).prop('disabled', false);
    
                    }
                 })
        })
    
        $("#post").click(function(event){
                event.preventDefault()
                console.log("hello")
                let noteId = $(this).val();
                let msg = $("#smsg").val();
                let email = $("#uemail").val()
                let datetime =  new Date().toLocaleString();
            
                $.ajax(
                    {
                        type:"POST",
                        enctype: 'multipart/form-data',
                        url: `/comment/${noteId}`,
                        data:{
                            csrfmiddlewaretoken: window.CSRF_TOKEN,
                            'notesid' : noteId, 
                            'msg' : msg,
                            'email':email,
                            'time' : datetime,             
                        },
                        datatype:'json',
                        success: function( data ) 
                        {
                            console.log("bal")
                            let div = document.createElement("div")
                            div.classList.add('comment', 'mt-4', 'text-justify')
                            let h4 = document.createElement("h4");
                            h4.innerHTML = email
                            let p1 = document.createElement("p");
                            let p2 = document.createElement("p");
                            p1.innerHTML = datetime
                            p2.innerHTML = msg
                            div.appendChild(h4)
                            div.appendChild(p1)
                            div.appendChild(p2)
                            console.log("done")
                            $("#cmntss").append(div)
                    }
                 })
            
        })

       
    
});



