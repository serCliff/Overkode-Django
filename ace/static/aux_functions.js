function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

function create_message(delta){
    msg = {}

    creation = {}
    creation['timestamp'] = Date.now();
    creation['user'] = user
    creation['action'] = delta['action']
    
    msg['creation'] = creation
    msg['content'] = delta

    return msg
};

