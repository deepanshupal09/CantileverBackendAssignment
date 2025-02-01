
import { DataSource } from 'typeorm';

export const databaseProviders = [
  {
    provide: 'DATA_SOURCE',
    useFactory: async () => {
      const dataSource = new DataSource({
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
