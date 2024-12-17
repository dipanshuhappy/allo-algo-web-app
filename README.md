# allo-algo-web-app

This repository provides a starter full-stack project based on AlgoKit, allowing you to quickly bootstrap and integrate Algorand-based functionalities into your own ecosystem. Fork it, customize strategies, interact with the registry, and build out your own decentralized applications on Algorand’s TestNet.

## How to Integrate into Your Project

1. **Fork This Repository**  
   Start by forking this repository into your own GitHub account. You will have a fully functional baseline that includes both smart contracts and a React-based frontend project.

2. **Create and Customize Your Strategy**  
   Within the `projects/allo-algo-web-app-contracts` directory, you’ll find a base strategy contract. Modify and extend this contract to implement your own custom logic—be it funding, grant distribution, or complex on-chain voting mechanisms.

3. **Interact with the Registry (App ID: 730129209)**  
   To manage identities and streamline user interactions on-chain, integrate with the provided registry contract on TestNet at **App ID 730129209**. Use the `createProfile` method on the registry contract to:
   - Register users or projects
   - Maintain structured, on-chain profiles for streamlined identity management

4. **Access the Quadratic Funding Strategy (App ID: 730129661)**  
   For advanced funding mechanisms, leverage the quadratic funding strategy at **App ID 730129661** on TestNet. This allows for:
   - More democratic fund distribution
   - Enhanced decision-making based on collective participant support

## Project Structure 
1. ***Contracts***
  within `/projects/allo-algo-web-app-contracts` , you have `base_strategy` which you can use to create your own allocation mechanism, and registry contract at `registry`
2. ***Frontend***
 within `/projects/allo-algo-web-app-frontend`. It implements  