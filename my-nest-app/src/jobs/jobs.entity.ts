import { Entity, Column, PrimaryColumn } from 'typeorm';

@Entity('jobs')
export class Job {
  @PrimaryColumn()
  apply_link: string;  

  @Column({ nullable: true })
  job_title: string; 
  
  @Column('text', { nullable: true })
  job_description: string;  

  @Column({ nullable: true })
  location: string;  

  @Column({ nullable: true })
  experience_level: string;  

  @Column({ nullable: true })
  company: string;  
}
