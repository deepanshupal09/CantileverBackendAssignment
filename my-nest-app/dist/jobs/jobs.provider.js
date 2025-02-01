"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.jobsProviders = void 0;
const jobs_entity_1 = require("./jobs.entity");
exports.jobsProviders = [
    {
        provide: 'JOBS_REPOSITORY',
        useFactory: (dataSource) => dataSource.getRepository(jobs_entity_1.Job),
        inject: ['DATA_SOURCE'],
    },
];
//# sourceMappingURL=jobs.provider.js.map