# Expense Tracker - System Diagrams

## 1. Entity Relationship (ER) Diagram
```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1f77b4',
    'primaryTextColor': '#fff',
    'primaryBorderColor': '#0d4875',
    'lineColor': '#2c3e50',
    'secondaryColor': '#3498db',
    'tertiaryColor': '#2ecc71'
  }
}}%%
erDiagram
    User ||--o{ Expense : "creates"
    Category ||--o{ Expense : "belongs to"
    User ||--o{ UserSession : "maintains"

    %% User Entity with Authentication
    User {
        int id PK "Auto increment"
        string username "Unique"
        string password "Hashed"
        string email "Optional"
        datetime date_joined "Auto now"
        boolean is_active "Default true"
        datetime last_login "Nullable"
    }

    %% Category Entity for Expense Classification
    Category {
        int id PK "Auto increment"
        string name "Unique"
        datetime created_at "Auto now"
        boolean is_default "Default false"
    }

    %% Main Expense Entity
    Expense {
        int id PK "Auto increment"
        int user_id FK "User reference"
        int category_id FK "Category reference"
        string title "Required"
        decimal amount "Precision(10,2)"
        string description "Optional"
        date date "Default today"
        time time "Default now"
        datetime created_at "Auto now"
        datetime updated_at "Auto now"
    }

    %% Session Management
    UserSession {
        int id PK "Auto increment"
        int user_id FK "User reference"
        string session_key "Unique"
        datetime created_at "Auto now"
        datetime expires_at "Configurable"
    }
```

## 2. UML Class Diagram
```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#2c3e50',
    'primaryTextColor': '#fff',
    'primaryBorderColor': '#2c3e50',
    'lineColor': '#34495e',
    'secondaryColor': '#3498db',
    'tertiaryColor': '#2ecc71'
  }
}}%%
classDiagram
    %% Abstract User class
    class AbstractUser {
        <<abstract>>
        -int id
        -str username
        -str password
        -str email
        -bool is_active
        -datetime last_login
        +authenticate(str, str) bool
        +check_password(str) bool
        +get_full_name() str
        +__str__() str
    }

    %% User class implementation
    class User {
        -list[Expense] expenses
        +create_expense(dict) Expense
        +get_expenses() list[Expense]
        +get_total_expenses() decimal
        +get_expenses_by_category(Category) list[Expense]
    }

    %% Category model
    class Category {
        -int id
        -str name
        -datetime created_at
        -bool is_default
        +__str__() str
        +get_expense_count() int
        +get_total_amount() decimal
    }

    %% Expense model with full features
    class Expense {
        -int id
        -str title
        -decimal amount
        -str description
        -User user
        -Category category
        -Date date
        -Time time
        -datetime created_at
        -datetime updated_at
        +__str__() str
        +formatted_amount() str
        +formatted_datetime() str
        +save() void
        +delete() void
        +update(dict) bool
    }

    %% Authentication manager
    class AuthManager {
        <<service>>
        +login(str, str) User
        +logout(User) void
        +register(dict) User
        +validate_password(str) bool
    }

    %% Relationships
    AbstractUser <|-- User : inherits
    User "1" -- "*" Expense : creates
    Category "1" -- "*" Expense : categorizes
    AuthManager -- User : manages
    
    %% Notes
    note for Category "Predefined and custom categories\nfor expense classification"
    note for Expense "Core entity for tracking\nfinancial transactions"
```

## 3. User Authentication Workflow
```mermaid
flowchart TD
    A[Start] --> B{User Logged In?}
    B -->|No| C[Display Login Form]
    B -->|Yes| D[Show Dashboard]
    
    C --> E{New User?}
    E -->|Yes| F[Display Signup Form]
    E -->|No| G[Enter Credentials]
    
    F --> H[Fill Registration Details]
    H --> I[Validate Input]
    I -->|Invalid| F
    I -->|Valid| J[Create Account]
    J --> G
    
    G --> K[Validate Credentials]
    K -->|Invalid| L[Show Error]
    L --> C
    K -->|Valid| D
    
    D --> M{Choose Action}
    M --> N[View Expenses]
    M --> O[Add Expense]
    M --> P[Generate Report]
    M --> Q[Use Calculators]
    M --> R[Logout]
    
    R --> B
```

## 2. Expense Management Workflow
```mermaid
flowchart TD
    A[Start] --> B[View Expense List]
    
    B --> C{Choose Action}
    
    C --> D[Add New Expense]
    D --> E[Enter Expense Details]
    E --> F[Select Category]
    F --> G[Enter Amount]
    G --> H[Add Description]
    H --> I[Set Date/Time]
    I --> J{Validate Input}
    J -->|Invalid| K[Show Error]
    K --> E
    J -->|Valid| L[Save Expense]
    L --> B
    
    C --> M[Delete Expense]
    M --> N{Confirm Delete}
    N -->|No| B
    N -->|Yes| O[Remove Expense]
    O --> B
    
    C --> P[Generate Report]
    P --> Q[Process Expenses]
    Q --> R[Create PDF]
    R --> S[Download Report]
    S --> B
```

## 3. PDF Generation Process
```mermaid
flowchart TD
    A[Start] --> B[Initialize PDF Document]
    B --> C[Add Header & Logo]
    C --> D[Add User Info]
    D --> E[Create Expense Table]
    
    E --> F[Process Each Expense]
    F --> G[Format Amount]
    G --> H[Format Date/Time]
    H --> I{More Expenses?}
    I -->|Yes| F
    I -->|No| J[Calculate Total]
    
    J --> K[Add Total Row]
    K --> L[Add Footer]
    L --> M[Generate PDF]
    M --> N[Return Response]
    N --> O[End]
```

## 4. Financial Calculator Flow
```mermaid
flowchart TD
    A[Start] --> B{Select Calculator}
    
    B --> C[Basic Calculator]
    C --> D[Enter Numbers]
    D --> E[Select Operation]
    E --> F[Show Result]
    
    B --> G[Split Bill]
    G --> H[Enter Total Amount]
    H --> I[Enter Number of People]
    I --> J[Show Per Person Amount]
    
    B --> K[GST Calculator]
    K --> L[Enter Base Amount]
    L --> M[Select GST Rate]
    M --> N[Show GST Amount]
    N --> O[Show Total Amount]
    
    B --> P[EMI Calculator]
    P --> Q[Enter Principal]
    Q --> R[Enter Interest Rate]
    R --> S[Enter Time Period]
    S --> T[Show Monthly EMI]
```

## How to Use These Flowcharts

1. These flowcharts are written in Mermaid.js format
2. To view them:
   - Use VS Code with Mermaid extension
   - Visit https://mermaid.live
   - Use any Markdown editor that supports Mermaid
3. To edit:
   - Edit the text between the ```mermaid tags
   - The syntax is simple and intuitive:
     - A --> B creates a flow from A to B
     - {text} creates a decision diamond
     - [text] creates a process box
     - |text| on arrows adds labels

## Flowchart Color Scheme Suggestions

For better visualization, you can add these styles in Mermaid:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#2c3e50',
    'primaryTextColor': '#fff',
    'primaryBorderColor': '#2c3e50',
    'lineColor': '#2c3e50',
    'secondaryColor': '#e74c3c',
    'tertiaryColor': '#18bc9c'
}}}%%
```

This will match your application's color scheme.