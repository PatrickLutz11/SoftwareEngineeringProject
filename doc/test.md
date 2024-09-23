# C3 [Components]: Static Structure

:::mermaid
---
title: TEST
---

%% type of graph
%% graph LR
graph TD



%% subgraphs
subgraph Extern[Extern]
    style Extern fill:#fa32ee

    E_A[User]
    end

subgraph Input[Input]
    style Input fill:#b238f7

    I_A[Input folder]
    I_B[Camera]
    end
subgraph DataSelector[Data Selector]
    S_A[One Image Selector]
    S_B[Webcam Snapshot]
    end
subgraph DataProcessor[Data Processor]
    style DataProcessor fill:#3ee6fa
    P_A[Object Pattern Recognition]
    P_B[Color Detection]
    P_C[Real-time Visualization]

    P_A --> P_B --> P_C
    end

subgraph Output[Output]
    style Output fill:#3efaa5

    O_A[Data Logger]
    O_B[CSV File]
    O_C[Display]
    O_A-->O_B
    
    end


%% main links
E_A -- Images --> I_A --> S_A -- image --> P_A
E_A -- enabling --> I_B --> S_B -- image --> P_A

P_A -- shape name --> O_A
P_B -- color --> O_A
P_C --> O_C

:::

