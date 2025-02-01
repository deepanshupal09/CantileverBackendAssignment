import { Inject, Injectable, Query } from '@nestjs/common';
import { Repository } from 'typeorm';
import { Job } from './jobs.entity';

@Injectable()
export class JobsService {
    constructor(
        @Inject('JOBS_REPOSITORY')
        private jobsRepository: Repository<Job>,
      ) {}

      async getJobs(company?: string): Promise<Job[]> {
        if (company) {
            company = company.toLowerCase().charAt(0).toUpperCase() + company.toLowerCase().slice(1);
            return this.jobsRepository.find({ where: { company } });
        }
        return this.jobsRepository.find();
      }
    
}
