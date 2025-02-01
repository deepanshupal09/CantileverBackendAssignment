import { Injectable } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';

@Injectable()
export class CronService {
  // Custom cron expression for every second
  @Cron(CronExpression.EVERY_12_HOURS)
  async handleCron() {
    try {
      console.log("Scraping initiated...");
      
      const response1 = fetch('http://127.0.0.1:5000/google-scraper?pages=2', { method: "GET" });
      const response2 = fetch('http://127.0.0.1:5000/deloitte-scraper?pages=2', { method: "GET" });

      await Promise.all([response1, response2]);

      console.log('Scrapers triggered successfully.');
    } catch (error) {
      console.error('Error triggering the scraper endpoints:', error);
    }
  }
}
