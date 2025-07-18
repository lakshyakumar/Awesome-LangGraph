# ✨ Contributing Guide ✨

Thanks for your interest in contributing! We welcome contributions of all kinds — bug reports, feature suggestions, code improvements, and more. Please read the guidelines below before getting started. 🚀

---

## 📚 Table of Contents

- [🍴 Fork the Repository](#-fork-the-repository)
- [📥 Clone Your Fork Locally](#-clone-your-fork-locally)
- [⏫ Set Upstream to Keep Your Fork Updated](#-set-upstream-to-keep-your-fork-updated)
- [📌 Issues & Locks](#-issues--locks)
  - [🔍 Looking for Issues?](#-looking-for-issues)
  - [🗝️ Want to Work on Something?](#️-want-to-work-on-something)
- [🌿 Branch and PR Guidelines](#-branch-and-pr-guidelines)
  - [🌱 Create a Feature Branch](#-create-a-feature-branch)
  - [🤘 Commit with Style](#-commit-with-style)
  - [📬 Create a Pull Request](#-create-a-pull-request)
- [✅ Code Style and Reviews](#-code-style-and-reviews)

---

## 🍴 Fork the Repository

Click the **Fork** button at the top right of the [repository page](https://github.com/your-repo-url). This creates your own copy of the repository under your GitHub account.

## 📥 Clone Your Fork Locally

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

## ⏫ Set Upstream to Keep Your Fork Updated

Add the original repository as the upstream remote:

```bash
git remote add upstream https://github.com/original-owner/original-repo.git
```

To pull changes from the upstream:

```bash
git fetch upstream
git checkout develop
git merge upstream/develop
```

---

## 📌 Issues & Locks

### 🔍 Looking for Issues?

- Check out [Issues](https://github.com/your-repo-url/issues) to find open tasks.
- Feel free to create new issues if something's missing!

### 🗝️ Want to Work on Something?

- Comment on an issue and **ask for a lock** 🔒 so others know you're working on it.
- If it’s a new task, create a new issue and ask for a lock on that.

---

## 🌿 Branch and PR Guidelines

### 🌱 Create a Feature Branch

Always branch from the `develop` branch:

```bash
git checkout develop
git checkout -b feat/your-feature-name
```

### 🤘 Commit with Style

Use expressive commit messages with emojis. Example:

```bash
git commit -m "🎉 Added the initial implementation of the login flow"
```

### 📬 Create a Pull Request

- Push your branch to your fork:

```bash
git push origin feat/your-feature-name
```

- Go to your fork on GitHub and click **Compare & Pull Request**
- Make sure the PR is targeting the `develop` branch
- Add a clear description of what your PR does

---

## ✅ Code Style and Reviews

- Keep your code clean and modular 🧼  
- Add comments if necessary 🗒️  
- Make sure to **add or update relevant documentation** for any new features, changes, or fixes you contribute 📝  
- Be open to feedback! 🙌

---

Thanks again for being awesome and contributing! 😎🔥