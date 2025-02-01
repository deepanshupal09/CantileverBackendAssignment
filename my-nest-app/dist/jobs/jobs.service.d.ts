import { Repository } from 'typeorm';
import { Job } from './jobs.entity';
export declare class JobsService {
    private jobsRepository;
    constructor(jobsRepository: Repository<Job>);
    getJobs(company?: string): Promise<Job[]>;
}
