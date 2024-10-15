module generator::RandomNumberGenerator {
    use aptos_framework::randomness;
    use aptos_framework::event;
    use std::signer;
    use std::error;

    // Struct to store the generated random value `r`
    struct GeneratedRandomValue has copy, drop, store {
        r: vector<u8>,  // Storing the random value as bytes
    }

    // Event emitted when the random value `r` is generated
    #[event]
    struct RandomValueGenerated has drop, store {
        account: address,
        r: vector<u8>,
    }

    // Resource to store the generated random value `r` for each user
    struct RandomValueStore has key {
        owner: address,
        generated_value: GeneratedRandomValue,
    }

    const ENO_USER_REGISTERED: u64 = 100;

    // Skip the unsafe randomness check
    #[lint::allow_unsafe_randomness]
    
    public entry fun generate_random_value(account: &signer) acquires RandomValueStore {
        // Generate a random value (e.g., 32 bytes)
        let r: vector<u8> = randomness::bytes(32);

        let generated_value = GeneratedRandomValue {
            r: r,
        };

        // Emit event with the generated random value
        event::emit(RandomValueGenerated {
            account: signer::address_of(account),
            r: r,
        });

        // Store the random value in the user's RandomValueStore resource
        let account_addr = signer::address_of(account);
        if (exists<RandomValueStore>(account_addr)) {
            let store = borrow_global_mut<RandomValueStore>(account_addr);
            store.generated_value = generated_value;
        } else {
            move_to(account, RandomValueStore {
                owner: account_addr,
                generated_value: generated_value,
            });
        }
    }

    // View function to retrieve the generated random value `r` for a given account
    public fun get_random_value(addr: address): vector<u8> acquires RandomValueStore {
        assert!(exists<RandomValueStore>(addr), error::not_found(ENO_USER_REGISTERED));
        borrow_global<RandomValueStore>(addr).generated_value.r
    }

    // Function to check if a random value has been generated for an account
    public fun has_random_value(addr: address): bool {
        exists<RandomValueStore>(addr)
    }
}
