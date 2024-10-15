module aggregator::aggregator {
    use std::signer;
    use std::vector;
    use std::error;
    use pedersen_commitment::generator;
    #[test_only]
    use std::debug;

    // Resource to store each node's commitment (Pedersen commitment)
    struct NodeCommitment has key {
        commitment: u64, // Simplified commitment value
    }

    // Resource to store the primes p and q
    struct AggregatorPrimes has key {
        p: u64,
        q: u64,
    }

    const ENO_COMMITMENT: u64 = 201;

    // Function to initialize the aggregator contract with the primes p and q
    public entry fun initialize_with_primes(account: signer, generator_addr: address) acquires AggregatorPrimes {
        let (p, q) = generator::get_primes(generator_addr);
        let account_addr = signer::address_of(&account);

        // Store primes in the aggregator contract
        if (!exists<AggregatorPrimes>(account_addr)) {
            move_to(&account, AggregatorPrimes {
                p,
                q,
            });
        }
    }

    // Function for nodes to submit their Pedersen commitment
    public entry fun submit_commitment(account: signer, commitment: u64) acquires NodeCommitment {
        let account_addr = signer::address_of(&account);

        if (!exists<NodeCommitment>(account_addr)) {
            move_to(&account, NodeCommitment {
                commitment,
            });
        } else {
            let node_commitment = borrow_global_mut<NodeCommitment>(account_addr);
            node_commitment.commitment = commitment;
        }
    }

    // Function to compute federated average and decrypt commitments
    public entry fun compute_federated_average(account: signer, nodes: vector<address>) 
    acquires NodeCommitment, AggregatorPrimes {
        let account_addr = signer::address_of(&account);
        let aggregator_primes = borrow_global<AggregatorPrimes>(account_addr);
        let p = aggregator_primes.p;
        let q = aggregator_primes.q;

        let total_commitment: u64 = 0;
        let node_count = vector::length(&nodes);

        for node_addr in &nodes {
            if (!exists<NodeCommitment>(*node_addr)) {
                continue;
            }
            let node_commitment = borrow_global<NodeCommitment>(*node_addr);
            let decrypted_value = decrypt_commitment(node_commitment.commitment, p, q);
            total_commitment = total_commitment + decrypted_value;
        }

        let average_commitment: u64 = total_commitment / node_count;

        // Log the result for testing
        debug::print(&string::utf8(b"Federated average decrypted value: "));
        debug::print_u64(average_commitment);
    }

    // Placeholder function for decrypting Pedersen commitment using primes p and q
    fun decrypt_commitment(commitment: u64, p: u64, q: u64): u64 {
        // This is a mock decryption function (you would replace this with the actual logic)
        // Example: commitment * inverse(p) mod q (simplified here for demo purposes)
        commitment // Return the decrypted value (mock logic here)
    }

    // Test function to simulate submission and averaging
    #[test(account = @0x1)]
    public entry fun test_federated_averaging(account: signer) acquires NodeCommitment, AggregatorPrimes {
        let node1 = signer::address_of(&account);
        let node2 = signer::address_of(&account);

        // Submit commitments from nodes
        submit_commitment(account, 100);
        submit_commitment(account, 200);

        // Simulate computing federated average
        let nodes: vector<address> = vector::from_elem(node1, 1);
        vector::push_back(&mut nodes, node2);

        compute_federated_average(account, nodes);
    }
}
