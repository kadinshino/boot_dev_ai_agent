# Agent Testing Suite

This is a comprehensive test suite for evaluating an agent's capabilities across file operations, code analysis, execution, debugging, and problem-solving tasks.

## 1. File Reading Tests

Test the agent's ability to explore and read files in the project structure.

```bash
python main.py "What files are in the calculator directory?"
python main.py "Show me the contents of calculator/pkg/render.py"
python main.py "What's in the lorem.txt file?"
```

## 2. Code Analysis Tests

Evaluate the agent's understanding of code logic and algorithms.

```bash
python main.py "Explain how the calculator precedence works"
python main.py "What algorithm does the calculator use?"
python main.py "Find any potential bugs in the calculator code"
```

## 3. Code Execution Tests

Test the agent's ability to run and interpret code execution results.

```bash
python main.py "Test the calculator with the expression 5 + 3 * 2"
python main.py "Run the calculator and show me what happens with division"
python main.py "Execute calculator/main.py with different test cases"
```

## 4. Bug Fixing Tests

Test debugging and problem-solving capabilities.

**Setup:** First, manually introduce a bug (e.g., change precedence values in `calculator.py`)

```bash
python main.py "Fix the bug: 2 + 3 * 4 should be 14, not 20"
python main.py "The calculator is giving wrong results for division"
```

## 5. File Modification Tests

Evaluate the agent's ability to make targeted file changes.

```bash
python main.py "Add a comment to the top of calculator.py explaining what it does"
python main.py "Create a new test file with some sample calculations"
python main.py "Modify the render function to use different box characters"
```

## 6. Multi-Step Problem Solving

Test complex, multi-step development tasks.

```bash
python main.py "Add support for the modulo operator (%) to the calculator"
python main.py "Create a backup of calculator.py before making changes"
python main.py "Add error handling for division by zero"
```

## 7. Cross-File Analysis

Evaluate understanding of project structure and dependencies.

```bash
python main.py "How does main.py connect to the calculator and render modules?"
python main.py "Are there any unused imports in the project?"
python main.py "What would happen if I deleted the render.py file?"
```

## 8. Stress Tests

Test performance with larger, more complex operations.

```bash
python main.py "List all Python files in the entire project and summarize what each does"
python main.py "Find and fix any style issues in the calculator code"
python main.py "Optimize the calculator for better performance"
```

## 9. Edge Case Tests

Evaluate handling of unusual inputs and error conditions.

```bash
python main.py "What happens if someone passes an empty expression to the calculator?"
python main.py "Handle the case where someone tries to divide by zero"
python main.py "Test the calculator with very large numbers"
```

## 10. Integration Tests

Test end-to-end functionality and component interaction.

```bash
python main.py "Make sure the calculator works with the fancy box rendering"
python main.py "Test that all the calculator functions work together properly"
```

## Usage

Run each test command individually to evaluate specific capabilities, or use them as part of an automated testing pipeline to assess overall agent performance across different domains.