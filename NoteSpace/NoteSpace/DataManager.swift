//
//  DataManager.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import Foundation
import Combine

class DataManager: ObservableObject {
    static let shared = DataManager()
    
    @Published var currentUser: User?
    @Published var spaces: [Space] = []
    @Published var notes: [Note] = []
    
    private let usersKey = "users"
    private let spacesKey = "spaces"
    private let notesKey = "notes"
    private let currentUserKey = "currentUser"
    
    init() {
        loadData()
    }
    
   
    func register(email: String, username: String, password: String) -> Bool {
        var users = getUsers()
        
       
        if users.contains(where: { $0.email == email }) {
            print("❌ User already exists: \(email)")
            return false
        }
        
        let newUser = User(
            id: UUID().uuidString,
            email: email,
            username: username,
            password: password, 
            spaceIds: []
        )
        
        users.append(newUser)
        saveUsers(users)
        print("✅ User registered: \(email)")
        
       
        let personalSpace = createSpace(
            name: "\(username)'s Space",
            description: "Personal space",
            creatorId: newUser.id
        )
        
        
        var updatedUser = newUser
        updatedUser.spaceIds.append(personalSpace.id)
        updateUser(updatedUser)
        
      
        currentUser = updatedUser
        saveCurrentUser(updatedUser)
        
       
        loadUserSpaces()
        
        return true
    }
    
    func login(email: String, password: String) -> Bool {
        let users = getUsers()
        
      
        if let user = users.first(where: { $0.email == email && $0.password == password }) {
            print("✅ User logged in: \(email)")
            currentUser = user
            saveCurrentUser(user)
            loadUserSpaces()
            return true
        }
        
        print("❌ Login failed for: \(email)")
        return false
    }
    
    func logout() {
        print("👋 User logged out: \(currentUser?.email ?? "unknown")")
        currentUser = nil
        UserDefaults.standard.removeObject(forKey: currentUserKey)
        spaces = []
        notes = []
    }
    
    func createSpace(name: String, description: String, creatorId: String) -> Space {
        var spaces = getSpaces()
        
        let newSpace = Space(
            id: UUID().uuidString,
            name: name,
            description: description,
            creatorId: creatorId,
            adminIds: [creatorId],
            memberIds: [creatorId],
            noteIds: [],
            inviteCode: generateInviteCode(),
            createdAt: Date()
        )
        
        spaces.append(newSpace)
        saveSpaces(spaces)
        print("✅ Space created: \(name) with code: \(newSpace.inviteCode)")
        
        return newSpace
    }
    
    func joinSpace(inviteCode: String, userId: String) -> Bool {
        var spaces = getSpaces()
        
        guard let index = spaces.firstIndex(where: { $0.inviteCode == inviteCode.uppercased() }) else {
            print("❌ Space not found with code: \(inviteCode)")
            return false
        }
        
        if spaces[index].memberIds.contains(userId) {
            print("⚠️ User already in space")
            return false
        }
        
        spaces[index].memberIds.append(userId)
        saveSpaces(spaces)
        print("✅ User added to space: \(spaces[index].name)")
        
        var users = getUsers()
        if let userIndex = users.firstIndex(where: { $0.id == userId }) {
            users[userIndex].spaceIds.append(spaces[index].id)
            saveUsers(users)
            
            if currentUser?.id == userId {
                currentUser = users[userIndex]
                saveCurrentUser(users[userIndex])
            }
        }
        
        loadUserSpaces()
        return true
    }
    
    func getSpaceMembers(spaceId: String) -> [User] {
        let allUsers = getUsers()
        guard let space = getSpaces().first(where: { $0.id == spaceId }) else {
            return []
        }
        
        return allUsers.filter { space.memberIds.contains($0.id) }
    }
    
    func canManageMembers(spaceId: String, userId: String) -> Bool {
        guard let space = getSpaces().first(where: { $0.id == spaceId }) else {
            return false
        }
        
        return space.creatorId == userId || space.adminIds.contains(userId)
    }
    
    func removeMemberFromSpace(spaceId: String, memberId: String) -> Bool {
        var spaces = getSpaces()
        
        guard let spaceIndex = spaces.firstIndex(where: { $0.id == spaceId }),
              let currentUserId = currentUser?.id,
              canManageMembers(spaceId: spaceId, userId: currentUserId) else {
            return false
        }
        
        if spaces[spaceIndex].creatorId == memberId {
            return false
        }
        
        spaces[spaceIndex].memberIds.removeAll { $0 == memberId }
        spaces[spaceIndex].adminIds.removeAll { $0 == memberId }
        saveSpaces(spaces)
        
        var users = getUsers()
        if let userIndex = users.firstIndex(where: { $0.id == memberId }) {
            users[userIndex].spaceIds.removeAll { $0 == spaceId }
            saveUsers(users)
        }
        
        if memberId == currentUserId {
            currentUser?.spaceIds.removeAll { $0 == spaceId }
        }
        
        loadUserSpaces()
        return true
    }
    
    func makeAdmin(spaceId: String, memberId: String) -> Bool {
        var spaces = getSpaces()
        
        guard let spaceIndex = spaces.firstIndex(where: { $0.id == spaceId }),
              let currentUserId = currentUser?.id,
              spaces[spaceIndex].creatorId == currentUserId else {
            return false
        }
        
        if !spaces[spaceIndex].adminIds.contains(memberId) && spaces[spaceIndex].memberIds.contains(memberId) {
            spaces[spaceIndex].adminIds.append(memberId)
            saveSpaces(spaces)
            loadUserSpaces()
            return true
        }
        
        return false
    }
    
    func removeAdmin(spaceId: String, memberId: String) -> Bool {
        var spaces = getSpaces()
        
        guard let spaceIndex = spaces.firstIndex(where: { $0.id == spaceId }),
              let currentUserId = currentUser?.id,
              spaces[spaceIndex].creatorId == currentUserId else {
            return false
        }
        
        if spaces[spaceIndex].adminIds.contains(memberId) && memberId != spaces[spaceIndex].creatorId {
            spaces[spaceIndex].adminIds.removeAll { $0 == memberId }
            saveSpaces(spaces)
            loadUserSpaces()
            return true
        }
        
        return false
    }
    
    func leaveSpace(spaceId: String, userId: String) -> Bool {
        var spaces = getSpaces()
        
        guard let spaceIndex = spaces.firstIndex(where: { $0.id == spaceId }) else {
            return false
        }
        
        if spaces[spaceIndex].creatorId == userId {
            return false
        }
        
        spaces[spaceIndex].memberIds.removeAll { $0 == userId }
        spaces[spaceIndex].adminIds.removeAll { $0 == userId }
        saveSpaces(spaces)
        
        var users = getUsers()
        if let userIndex = users.firstIndex(where: { $0.id == userId }) {
            users[userIndex].spaceIds.removeAll { $0 == spaceId }
            saveUsers(users)
        }
        
        if userId == currentUser?.id {
            currentUser?.spaceIds.removeAll { $0 == spaceId }
        }
        
        loadUserSpaces()
        return true
    }
    
    func getSpaceInviteLink(spaceId: String) -> String {
        let spaces = getSpaces()
        if let space = spaces.first(where: { $0.id == spaceId }) {
            return "notespace://join/\(space.inviteCode)"
        }
        return ""
    }
    
    func createNote(title: String, content: String, spaceId: String, authorId: String, authorName: String) {
        var notes = getNotes()
        
        let newNote = Note(
            id: UUID().uuidString,
            title: title,
            content: content,
            authorId: authorId,
            authorName: authorName,
            spaceId: spaceId,
            createdAt: Date(),
            updatedAt: Date()
        )
        
        notes.append(newNote)
        saveNotes(notes)
        
        var spaces = getSpaces()
        if let index = spaces.firstIndex(where: { $0.id == spaceId }) {
            spaces[index].noteIds.append(newNote.id)
            saveSpaces(spaces)
        }
        
        loadUserSpaces()
    }
    
    func updateNote(noteId: String, title: String, content: String) {
        var notes = getNotes()
        
        if let index = notes.firstIndex(where: { $0.id == noteId }) {
            notes[index].title = title
            notes[index].content = content
            notes[index].updatedAt = Date()
            saveNotes(notes)
        }
        
        loadUserSpaces()
    }
    
    func deleteNote(noteId: String, spaceId: String) {
        var notes = getNotes()
        notes.removeAll { $0.id == noteId }
        saveNotes(notes)
        
        var spaces = getSpaces()
        if let index = spaces.firstIndex(where: { $0.id == spaceId }) {
            spaces[index].noteIds.removeAll { $0 == noteId }
            saveSpaces(spaces)
        }
        
        loadUserSpaces()
    }
    
    func loadUserSpaces() {
        guard let user = currentUser else {
            print("⚠️ No current user")
            return
        }
        
        let allSpaces = getSpaces()
        spaces = allSpaces.filter { user.spaceIds.contains($0.id) }
        
        let allNotes = getNotes()
        notes = allNotes.filter { note in
            spaces.contains { $0.noteIds.contains(note.id) }
        }
        
        print("📊 Loaded \(spaces.count) spaces for user \(user.username)")
    }
    
    private func generateInviteCode() -> String {
        let letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return String((0..<6).map { _ in letters.randomElement()! })
    }
    
    private func getUsers() -> [User] {
        guard let data = UserDefaults.standard.data(forKey: usersKey),
              let users = try? JSONDecoder().decode([User].self, from: data) else {
            return []
        }
        return users
    }
    
    private func saveUsers(_ users: [User]) {
        if let data = try? JSONEncoder().encode(users) {
            UserDefaults.standard.set(data, forKey: usersKey)
        }
    }
    
    private func getSpaces() -> [Space] {
        guard let data = UserDefaults.standard.data(forKey: spacesKey),
              let spaces = try? JSONDecoder().decode([Space].self, from: data) else {
            return []
        }
        return spaces
    }
    
    private func saveSpaces(_ spaces: [Space]) {
        if let data = try? JSONEncoder().encode(spaces) {
            UserDefaults.standard.set(data, forKey: spacesKey)
        }
    }
    
    private func getNotes() -> [Note] {
        guard let data = UserDefaults.standard.data(forKey: notesKey),
              let notes = try? JSONDecoder().decode([Note].self, from: data) else {
            return []
        }
        return notes
    }
    
    private func saveNotes(_ notes: [Note]) {
        if let data = try? JSONEncoder().encode(notes) {
            UserDefaults.standard.set(data, forKey: notesKey)
        }
    }
    
    private func updateUser(_ user: User) {
        var users = getUsers()
        if let index = users.firstIndex(where: { $0.id == user.id }) {
            users[index] = user
            saveUsers(users)
        }
    }
    
    private func saveCurrentUser(_ user: User) {
        if let data = try? JSONEncoder().encode(user) {
            UserDefaults.standard.set(data, forKey: currentUserKey)
        }
    }
    
    private func loadData() {
        if let data = UserDefaults.standard.data(forKey: currentUserKey),
           let user = try? JSONDecoder().decode(User.self, from: data) {
            currentUser = user
            loadUserSpaces()
            print("🔄 Loaded saved user: \(user.username)")
        }
    }
}
