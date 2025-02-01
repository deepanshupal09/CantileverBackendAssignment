import { DataSource } from 'typeorm';
import { Job } from './jobs.entity';

export const jobsProviders = [
  {
    provide: 'JOBS_REPOSITORY',
    useFactory: (dataSource: DataSource) => dataSource.getRepository(Job),
    inject: ['DATA_SOURCE'],
  },
];
