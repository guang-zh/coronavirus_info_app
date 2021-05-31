'use strict'

document.addEventListener('DOMContentLoaded', setUp);

// global variables(paragraph)
let msg_notifications = document.querySelectorAll('.msgs');

/**
 * @author Yassine Ibhir
 * setUp function calls fetchNumberMessages method
 */
function setUp(){
    fetchNumberMessages();
}

/**
fetch number of messages from django view
*/
function fetchNumberMessages(){
    let url = "/message_app/messages_num/"
    fetch(url).then(response => {
        if(!response.ok){
            throw new Error('status code:'+ response.status);
        }
        return response.json();
    })
    .then(json =>{
        setNotification(json);
    })

    .catch(error => console.log(error));

}

/**
set number of unread messages
*/
function setNotification(obj){
    for (let i = 0; i < msg_notifications.length; i++) {
        msg_notifications[i].textContent = obj.unread_msgs;
        msg_notifications[i].style.color = "#00ff80";
    }

}

// Project comment/like/rate functionalities


