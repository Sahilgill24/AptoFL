module generator::GeneratorContract {
    use aptos_framework::account;
    use aptos_framework::signer;
    use std::error;
    use aptos_std::vector;

    /// Primes and generators used for Pedersen commitments
    struct Parameters has key {
        p: u64,
        q: u64,
        g: u64,
        h: u64,
    }

    /// Error codes
    const E_ALREADY_REGISTERED: u64 = 1;

    /// Registers the generator parameters `p`, `q`, `g`, `h`.
    public entry fun setup(account: signer, p: u64, q: u64, g: u64, h: u64) acquires Parameters {
        let account_addr = signer::address_of(&account);
        
        // Ensure parameters are not already registered
        if (exists<Parameters>(account_addr)) {
            assert!(false, E_ALREADY_REGISTERED);
        };
        
        move_to(&account, Parameters { p:p, q:q, g:g, h:h });
    }

    /// Returns the registered parameters
    public fun get_parameters(account: &signer): (u64, u64, u64, u64) acquires Parameters {
        let account_addr = signer::address_of(account);
        let params = borrow_global<Parameters>(account_addr);
        (params.p, params.q, params.g, params.h)
    }
}
