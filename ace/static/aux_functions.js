function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

function create_message(delta){
    msg = {}

    creation = {}
    creation['timestamp'] = "now"
    creation['user'] = user
    creation['action'] = delta['action']

    // rcv = {}
    // rcv['id'] = user
    // rcv['username'] = "Anonymous"
    // rcv['port'] = 
    
    // msg['receivers'] = {}
    // msg['receivers'][user] = rcv
    
    msg['creation'] = creation

    msg['content'] = delta

    return msg
};

