import { DataSource } from 'typeorm';
import { Job } from './jobs.entity';
export declare const jobsProviders: {
    provide: string;
    useFactory: (dataSource: DataSource) => import("typeorm").Repository<Job>;
    inject: string[];
}[];
