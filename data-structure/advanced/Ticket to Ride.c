#include <stdio.h>
#include <string.h>
#include <stdlib.h>
static void _propogate(
    long *max,
    long *pending,
    unsigned length,
    unsigned at
) {    
    unsigned root;
    unsigned short levels = __builtin_clz(length) ^ 31U;
    for (; levels; levels--)
        if (pending[at >> levels]) {                        
            root = at >> (levels - 1);
            max[root] += pending[root >> 1];
            pending[root] += pending[root >> 1];                        
            
            max[root ^ 1] += pending[root >> 1];
            pending[root ^ 1] += pending[root >> 1];
            pending[root >> 1] = 0;
        }
}

static inline long query_largest(
    long *max,
    long *pending,
    unsigned length
) {
    _propogate(max, pending, length, (length << 1) - 1);       
    long largest = 0x8000000000000000L;
    unsigned low = length; 
    for (length <<= 1; low < length; low >>= 1, length >>= 1) {
        if (low & 1 && largest < max[low++])
            largest = max[low - 1];
        if (length & 1 && largest < max[length ^= 1])
            largest = max[length];
    }
    return largest;
}

static void update_range(
    long *max,
    long *pending,
    unsigned length,
    unsigned low,
    unsigned high,
    long delta
) {
    unsigned 
        at_low = (low += length), 
        at_high = (high += (length - 1)) + 1;

    for (; at_low < at_high; at_low >>= 1, at_high >>= 1) {
        if (at_low & 1) {
            max[at_low] += delta;            
            pending[at_low++] += delta;
        }
        if (at_high & 1) {
            max[at_high ^= 1] += delta;
            pending[at_high] += delta;
        }        
    }

    for (; low > 1; low >>= 1)
        max[low >> 1] = pending[low >> 1] + max[low ^ (max[low ^ 1] > max[low])];
    
    for (; high > 1; high >>= 1)
        max[high >> 1] = pending[high >> 1] + max[high ^ (max[high ^ 1] > max[high])];
}

int main() {    
    unsigned vertex_cnt;
    scanf("%u", &vertex_cnt);

    unsigned 
        at, others, next, tail, length,
        ancestors[vertex_cnt],
        lengths[vertex_cnt << 1];
    
    memset(lengths, 0, vertex_cnt * sizeof(lengths[0]));
    for (at = vertex_cnt; --at; ancestors[others] = tail, lengths[others] = length)
        if (lengths[(scanf("%u %u %u", &tail, &others, &length), --tail, --others)])
            for (next = tail, tail = others, others = next; lengths[others]; others = next) {                
                next = lengths[others];
                lengths[others] = length;
                length = next;

                next = ancestors[others];                
                ancestors[others] = tail;
                tail = others;
            } 

    for (; lengths[at]; at = ancestors[at]);
    ancestors[at] = vertex_cnt;

    unsigned 
        indices[vertex_cnt + 2],
        neighbors[vertex_cnt << 1];    

    memset(indices, 0, sizeof(indices));
    for (at = vertex_cnt; at--; *(unsigned long *)&indices[ancestors[at]] += 0x100000001UL);
    for (; ++at < (vertex_cnt >> 1); ((unsigned long *)indices)[at + 1] += ((unsigned long *)indices)[at]);
    for (at = vertex_cnt; at--; neighbors[--indices[ancestors[at]]] = at);
    lengths[neighbors[vertex_cnt - 1]] = 0;

    unsigned
        history[vertex_cnt],
        weights[vertex_cnt + 1];
    
    at += vertex_cnt;
    for (history[at] = neighbors[at], others = 0; others < at; others++) {
        history[others] = history[at];
        at -= (indices[history[others] + 1] - indices[history[others]]) - 1;
        memcpy(
            &history[at],
            &neighbors[indices[history[others]]],
            (indices[history[others] + 1] - indices[history[others]]) * sizeof(history[0])
        );
    }    
    *(unsigned long *)&weights[vertex_cnt - 1] = 1UL;
    for (at = vertex_cnt >> 1; at--; ((unsigned long *)weights)[at] = 0x100000001UL);
    for (at = vertex_cnt; --at; weights[ancestors[history[at]]] += weights[history[at]])
        ;

    {
        unsigned 
            centroids[vertex_cnt],
            mass[vertex_cnt];

        at = vertex_cnt - 1;
        history[at] = neighbors[at];
        centroids[history[at]] = (mass[history[at]] = vertex_cnt);

        for (length = 0; length < at; weights[(history[length++] = next)] = 0) {
            for (tail = (next = history[at]); (weights[next] << 1) < mass[history[at]]; next = ancestors[tail = next]);
            for (others = indices[next]; others < indices[next + 1]; others++)
                if ((weights[neighbors[others]] << 1) > mass[history[at]] && neighbors[others] != tail) 
                    others = indices[next = neighbors[others]] - 1;
            
            mass[next] = mass[history[at]];
            for (centroids[next] = centroids[history[at++]]; others-- > indices[next]; ) 
                if (weights[neighbors[others]]) {
                    centroids[history[--at] = neighbors[others]] = next;          
                    mass[history[at]] = weights[neighbors[others]];      
                }
            for (others = next; weights[ancestors[others]]; weights[others = ancestors[others]] -= weights[next]);
            if (others != next) {
                centroids[history[--at] = ancestors[next]] = next;
                mass[history[at]] = weights[others];                            
            }            
        }
        memcpy(weights, mass, sizeof(mass));
    }            

    for (tail = vertex_cnt, at = history[length = 0]; at != vertex_cnt; at = next) {
        next = lengths[at];
        lengths[at] = length;
        length = next;

        next = ancestors[at];
        ancestors[at] = tail;
        tail = at;        
    }    
        
    for (indices[at] = 0; at--; history[at] = lengths[history[at]]) 
        indices[history[at]] = at;        

    memcpy(neighbors, ancestors, vertex_cnt * sizeof(ancestors[0]));
    for (at = vertex_cnt; at--; ancestors[indices[at]] = indices[neighbors[at]]);

    scanf("%u", &length); 
    unsigned                    
        *locations = memset(
            malloc(((length << 2) + ((vertex_cnt << 1) + 2)) * sizeof(locations[0])), 
            0, 
            (vertex_cnt + 2) * sizeof(locations[0])
        ),
        *mass = &locations[vertex_cnt + 2],
        *dests = &mass[vertex_cnt],
        *costs = &dests[length << 1];            
    {
        unsigned 
            sources[length],
            targets[length],
            prices[length];

        for (at = length; at--; ) {
            scanf("%u %u %u", &tail, &others, &prices[at]);

            *(unsigned long *)&locations[sources[at] = indices[tail - 1]] += 0x100000001UL;
            *(unsigned long *)&locations[targets[at] = indices[others - 1]] += 0x100000001UL;            
        }
        for (; ++at < (vertex_cnt >> 1); ((unsigned long *)locations)[at + 1] += ((unsigned long *)locations)[at]);
        for (at = length; at--; ) {
            dests[--locations[targets[at]]] = sources[at];
            dests[--locations[sources[at]]] = targets[at];

            costs[locations[sources[at]]] = prices[at];
            costs[locations[targets[at]]] = prices[at];
        }         
    }  

    memcpy(lengths, weights, vertex_cnt * sizeof(weights[0]));
    for (at = vertex_cnt; at--; mass[indices[at]] = lengths[at]);      

    for (at = vertex_cnt >> 1; --at; ((unsigned long *)indices)[at] = 0x200000002UL);    
    *(unsigned long *)&indices[vertex_cnt - 1] = 0x100000002UL;   
    *(unsigned long *)indices = 0x100000000UL;

    for (at = vertex_cnt; --at; *(unsigned long *)&indices[ancestors[at]] += 0x100000001UL);        
    for (; ++at <= (vertex_cnt >> 1); ((unsigned long *)indices)[at] += ((unsigned long *)indices)[at - 1]);        
    for (at = vertex_cnt; --at; lengths[indices[ancestors[at]]] = history[at])       
        neighbors[--indices[ancestors[at]]] = at;        

    for (at = vertex_cnt; --at; neighbors[others - 1] = ancestors[at], lengths[others - 1] = history[at]) 
        for (others = --indices[at]; 
             ++others < indices[at + 1] && neighbors[others] < ancestors[at]; 
             lengths[others - 1] = lengths[others]
        ) neighbors[others - 1] = neighbors[others];
        
    unsigned
        seen[(vertex_cnt >> 5) + 1],        
        *ids = malloc(11 * vertex_cnt * sizeof(ids[0]));                    

    long                 
        *total_costs = (long *)&ids[vertex_cnt],
        *max_profits = &total_costs[vertex_cnt],
        *pending = &max_profits[vertex_cnt << 1],        
        max = 0;    
    
    memset(ids, 0xFFU, vertex_cnt * sizeof(ids[0]));    
    memset(seen, 0, sizeof(seen));    
    #define have(self, id) ((self)[(id) >> 5] &  (1U << ((id) & 31U)))
    #define flip(self, id) ((self)[(id) >> 5] ^= (1U << ((id) & 31U)))    

    for (tail = 0; tail < vertex_cnt; tail++) {                          
        memset(&weights[tail], 0, mass[tail] * sizeof(weights[0]));        
        
        weights[tail] = 1;
        total_costs[tail] = 0;
        history[at = (mass[tail] - 1)] = tail;
        for (next = 0; next < at; next++)
            for (others = indices[(history[next] = history[at++])]; others < indices[history[next] + 1]; others++) 
                if (weights[neighbors[others]] == 0) {
                    weights[history[--at] = neighbors[others]] = 1;
                    ancestors[history[at]] = history[next];
                    total_costs[history[at]] = total_costs[history[next]] - lengths[others];                       
                }
        
        for (max_profits += (at = mass[tail]); --at; ids[history[at]] = at) {
            weights[ancestors[history[at]]] += weights[history[at]];
            max_profits[at] = total_costs[history[at]];
        }                        
        max_profits[(ids[tail] = 0)] = 0;

        memset(&total_costs[tail], 0, mass[tail] * sizeof(total_costs[0]));                        
        for (ancestors[tail] = tail; at < mass[tail]; at++) {
            for (others = locations[history[at]]; others < locations[history[at] + 1]; others++)
                if (ids[dests[others]] > ids[history[at]] && ids[dests[others]] < (ids[history[at]] + weights[history[at]]))
                    total_costs[dests[others]] += costs[others];
            
            total_costs[history[at]] += total_costs[ancestors[history[at]]];
            max_profits[at] += total_costs[history[at]];            
            if (max < max_profits[at])
                max = max_profits[at];
        }
        for (; at--; total_costs[history[at]] = max_profits[at]);
        max_profits -= mass[tail];

        for (memset(pending, 0, (at = (mass[tail] << 1)) * sizeof(pending[0])); at-- > 1;
            max_profits[at >> 1] = max_profits[at ^ (max_profits[at ^ 1] > max_profits[at])]);
                           
        for (others = indices[tail + 1]; others-- > indices[tail]; )
            if (have(seen, neighbors[others]) == 0)                                
                history[at++] = neighbors[others];        
        ids[tail] = 0xFFFFFFFFU;
        for (flip(seen, tail); at--; at = next) {            
            update_range(
                max_profits, pending, mass[tail],
                ids[history[at]], ids[history[at]] + weights[history[at]], 
                -200000000000000L
            );
            long max_seen = query_largest(max_profits, pending, mass[tail]);
            for (next = at++; at-- != next; ) 
                if (have(seen, history[at])) {
                    flip(seen, history[at]);
                    length = 0;
                    for (others = locations[history[at]]; others < locations[history[at] + 1]; others++)
                        if (ids[dests[others]] < ids[history[next]]) {
                            update_range(
                                max_profits, pending, mass[tail],
                                ids[dests[others]], ids[dests[others]] + weights[dests[others]],
                                -(long)costs[others]
                            );
                            length = 1;
                        }
                    if (length)
                        max_seen = query_largest(max_profits, pending, mass[tail]);
                } else {
                    flip(seen, history[at]);
                    
                    length = 0;
                    for (others = locations[history[at]]; others < locations[history[at] + 1]; others++)
                        if (ids[dests[others]] < ids[history[next]]) {
                            update_range(
                                max_profits, pending, mass[tail],
                                ids[dests[others]], ids[dests[others]] + weights[dests[others]],
                                costs[others]
                            );
                            length = 1;
                        }
                    if (length)
                        max_seen = query_largest(max_profits, pending, mass[tail]);
                    
                    if (max < (max_seen + total_costs[history[at]]))
                        max = max_seen + total_costs[history[at]];
                    
                    for (others = indices[history[at]], length = indices[history[at++] + 1]; others < length; others++)
                        if (have(seen, neighbors[others]) == 0)
                            history[at++] = neighbors[others];
                }            
            update_range(
                max_profits, pending, mass[tail], 
                ids[history[next]], ids[history[next]] + weights[history[next]],
                200000000000000L
            );
        }
        memset(&ids[tail], 0xFFU, mass[tail] * sizeof(ids[0]));
    }    

    printf("%ld", max);
    
    free(ids);
    free(locations);
    return 0;
}