import { Controller, Get, Query } from '@nestjs/common';
import { JobsService } from './jobs.service';
import { Job } from './jobs.entity';


@Controller('jobs')
export class JobsController {

    constructor(private readonly jobsService: JobsService) {}

    @Get()
    getJobs(@Query('company') company?: string): Promise<Job[]> {
        return this.jobsService.getJobs(company);
    }   
}
