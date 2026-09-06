# Shared Household Chores Tool

## Purpose

Build a simple tool for one household to organize shared chores, rotate responsibility fairly, and track completion.

## Target Users

- One household
- Up to five household members
- Members use a shared device
- No accounts or login required

## Core Features

1. Manage household members
	- Add members
	- Remove members
	- Rename members
	- Anyone can manage members

2. Create and edit chores
	- Support predefined chores and custom chores
	- Each chore has a name, assignee, due date, and recurring schedule
	- Support daily, weekly, and monthly schedules
	- Anyone can add, edit, and delete chores

3. Rotate chore assignments automatically
	- Recurring chores rotate among household members
	- Each chore has exactly one assignee
	- Users can filter the chore list by person

4. Track chore status and workload
	- Anyone can mark a chore complete
	- Completed chores remain visible in recent history
	- Overdue chores receive an overdue label
	- The main view emphasizes each person's workload

## Platform and Storage

- Local, mobile-friendly web app
- Data persists in the local SQLite database managed by Django

## Out of Scope for the MVP

- User accounts and authentication
- Email or push notifications
- Points, streaks, leaderboards, or rewards
- Skipping or deferring chores
- Swapping chores between members
- External production database

## MVP Success Criteria

- A household can add its members.
- A member can create a one-time or recurring chore.
- The app assigns recurring chores according to the rotation.
- Household members can see workload by person.
- Anyone can mark chores complete.
- The app identifies overdue chores and preserves recent completion history.
