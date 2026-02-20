//
//  ContentView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject private var dataManager: DataManager
    
    var body: some View {
        if dataManager.currentUser != nil {
            MainTabView()
        } else {
            AuthView()
        }
    }
}
