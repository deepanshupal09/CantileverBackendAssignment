import { JobsService } from './jobs.service';
import { Job } from './jobs.entity';
export declare class JobsController {
    private readonly jobsService;
    constructor(jobsService: JobsService);
    getJobs(company?: string): Promise<Job[]>;
}
