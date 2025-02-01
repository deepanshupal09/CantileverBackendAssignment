"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.databaseProviders = void 0;
const typeorm_1 = require("typeorm");
exports.databaseProviders = [
    {
        provide: 'DATA_SOURCE',
        useFactory: async () => {
            const dataSource = new typeorm_1.DataSource({
                type: 'postgres',
                host: 'dpg-cuf26956l47c73fabv00-a.singapore-postgres.render.com',
                port: 5432,
                username: 'deepanshupal',
                password: 'NyVoSBDZhnRgKKMg7lHSdU57Kc76VaK4',
                database: 'scrapper_tztj',
                entities: [
                    __dirname + '/../**/*.entity{.ts,.js}',
                ],
                synchronize: true,
                ssl: {
                    rejectUnauthorized: true,
                }
            });
            return dataSource.initialize();
        },
    },
];
//# sourceMappingURL=database.providers.js.map