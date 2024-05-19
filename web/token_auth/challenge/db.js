const mysql = require("mysql2/promise");

require("dotenv").config();

const config = {
    host: "127.0.0.1",
    user: "user",
    password: "25CdBXS3ACGCnZ4sPTvTV8hJ",
    database: "token_auth",
    connectTimeout: 60000,
    socketPath: '/var/run/mysqld/mysqld.sock'
};

async function query(sql, params) {
    if (!params) {
        params = [];
    }
    params = params.map((param) => {
        return param.toString();
    });

    try {
        const connection = await mysql.createConnection(config);
        const [results] = await connection.execute(sql, params);
        return results;
    } catch (error) {
        console.log("Database error:", error);
        throw error;
    }
}

query(`CREATE TABLE IF NOT EXISTS \`users\` (
    \`id\` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    \`username\` varchar(255) NOT NULL,
    \`password\` varchar(255) NOT NULL,
    \`role\` varchar(10) DEFAULT NULL
);`);

module.exports = query;
