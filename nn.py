import getpass
import readDB
import readTestDB
import parseData
import createDicts
import tensorflow as tf
import csv


def train_model(names_dict, teams_dict):
    reg_factor = 0.001
    batch_size = 50
    iterations = 75000

    # Start tensorflow model
    feature_count = len(names_dict) + (2*len(teams_dict)) + 6 + 34
    x = tf.placeholder(tf.float32, shape=[None, feature_count])
    y_ = tf.placeholder(tf.float32, shape=[None, 1])

    # First fully connected layer: ReLU
    W_fc1 = tf.Variable(tf.truncated_normal([feature_count, 1024], stddev=0.1))
    b_fc1 = tf.Variable(tf.constant(0.1, shape=[1024]))
    h_fc1 = tf.nn.relu(tf.matmul(x, W_fc1) + b_fc1)

    # Second fully connected layer: ReLU + Dropout
    W_fc2 = tf.Variable(tf.truncated_normal([1024, 128], stddev=0.1))
    b_fc2 = tf.Variable(tf.constant(0.1, shape=[128]))
    h_fc2 = tf.nn.relu(tf.matmul(h_fc1, W_fc2) + b_fc2)

    keep_prob = tf.placeholder(tf.float32)
    h_drop = tf.nn.dropout(h_fc2, keep_prob)

    # Final fully connected layer
    W_fc3 = tf.Variable(tf.truncated_normal([128, 1], stddev=0.1))
    b_fc3 = tf.Variable(tf.constant(0.1, shape=[1]))
    y_nn = tf.matmul(h_drop, W_fc3) + b_fc3



    # Define Loss Function
    loss_original = tf.reduce_mean(tf.square(y_ - y_nn))
    loss_abs = tf.reduce_mean(tf.abs(y_ - y_nn))
    regularizer = tf.nn.l2_loss(W_fc1) + tf.nn.l2_loss(W_fc2) +\
                  tf.nn.l2_loss(W_fc3) + tf.nn.l2_loss(b_fc1) +\
                  tf.nn.l2_loss(b_fc2) + tf.nn.l2_loss(b_fc3)
    learning_rate = tf.placeholder(tf.float32, shape=[])
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    loss = tf.reduce_mean(loss_original + reg_factor * regularizer)
    train_step = optimizer.minimize(loss)


    print("TRAINING STARTED")
    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())

    for step in range(1, iterations):
        # Read some random entries from DB
        query_result = readDB.readDB(batch_size)
        # Parse data to convert names into numbers
        batch_x, batch_y = parseData.parseData(query_result, names_dict, teams_dict)
        
        if step % 250 == 0:
            print("\nStep: %d"%step)
            test_query_result = readTestDB.readTestDB(30)
            test_x, test_y = parseData.parseData(test_query_result, names_dict, teams_dict)
            dic = {x:batch_x, y_:batch_y, keep_prob:1.0}
            train_mean = loss_original.eval(feed_dict=dic)
            print("Training set MSE: %g" %train_mean)
            train_mean_reg = loss.eval(feed_dict=dic)
            print('Trainin set MSE+reg: %g' %train_mean_reg)
            dic_test = {x:test_x, y_:test_y, keep_prob:1.0}
            test_mean = loss_original.eval(feed_dict=dic_test)
            print("Validation set MSE: %g" %test_mean)
            test_mean_abs = loss_abs.eval(feed_dict=dic_test)
            print("Validation set MAE: %g" %test_mean_abs)
            print(test_y[:5])
            print(y_nn.eval(feed_dict={x:test_x, keep_prob:1.0})[:5])

        # Update learning rate
        if step < 10000:
            learning_r = 0.01
        elif step < 25000:
            learning_r = 0.001
        else:
            learning_r = 0.0001

        # Train on current batch
        train_data = {x:batch_x, y_:batch_y, keep_prob:0.5, learning_rate:learning_r}
        train_step.run(feed_dict=train_data)



