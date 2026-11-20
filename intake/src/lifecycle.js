// Central lifecycle rules for the generic intake ledger.
const allowed={
 accepted:["queued","blocked_infrastructure","cancelled"],
 queued:["processing","failed_retryable","failed_terminal","blocked_infrastructure","cancelled"],
 processing:["completed","failed_retryable","failed_terminal","blocked_infrastructure","cancelled"],
 failed_retryable:["queued","processing","failed_terminal","cancelled"],
 blocked_infrastructure:["queued","processing","cancelled"],
 completed:[],failed_terminal:[],cancelled:[]
};
export function canTransition(from,to){return !!allowed[from]?.includes(to);}
export function transition(from,to){if(!canTransition(from,to))throw new Error("invalid_job_transition");return to;}
export function isTerminal(status){return ["completed","failed_terminal","cancelled"].includes(status);}
export function retryDisposition(status,attempts,maxAttempts=5){if(isTerminal(status))return "terminal";if(status==="blocked_infrastructure")return "owner_action";if(attempts>=maxAttempts)return "terminalize";return "retry";}
