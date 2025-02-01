import { Module } from '@nestjs/common';
import { DatabaseModule } from '../database/database.module';
import { JobsService } from './jobs.service';
import { JobsController } from './jobs.controller';
import { jobsProviders } from './jobs.provider';

@Module({
  imports: [DatabaseModule],
  providers: [
    ...jobsProviders,
    JobsService,
  ],
  controllers: [JobsController],
})
export class JobsModule {}
